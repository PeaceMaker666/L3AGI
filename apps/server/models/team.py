from __future__ import annotations
from typing import List, Optional
import uuid

from sqlalchemy import Column, String, Boolean, UUID, func, or_, ForeignKey, Integer
from sqlalchemy.orm import relationship
from models.base_model import BaseModel
from l3_types.team_types import TeamInput
from exceptions import TeamNotFoundException

class TeamModel(BaseModel):
    """
    Represents an team entity.

    Attributes:
        id (UUID): Unique identifier of the team.
        name (str): Name of the team.

    """
    __tablename__ = 'team'

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String)
    type = Column(String) #todo replace as enum (Debates, Plan_Execute, Authoritarian_Speaker, Decentralized_speaker)
    description = Column(String, nullable=True) 
    is_deleted = Column(Boolean, default=False)
    is_system = Column(Boolean, default=False)
    is_template = Column(Boolean, default=False)
    project_id = Column(UUID, ForeignKey('project.id'), nullable=True) 
    account_id = Column(UUID, ForeignKey('account.id'), nullable=True)
    
    account = relationship("AccountModel", cascade="all, delete")
    team_agents = relationship("TeamAgentModel", back_populates="team")
    
    def __repr__(self) -> str:
        return (
            f"Team(id={self.id}, "
            f"name='{self.name}', type='{self.type}', description='{self.description}', "
            f"is_deleted={self.is_deleted}, is_system={self.is_system}, is_template={self.is_template}, "
            f"project_id={self.project_id}, account_id={self.account_id})"
        )

    @classmethod
    def create_team(cls, db, team, user, account):
        """
        Creates a new team with the provided configuration.

        Args:
            db: The database object.
            team_with_config: The object containing the team and configuration details.

        Returns:
            Team: The created team.

        """
        db_team = TeamModel(
                         created_by=user.id, 
                         account_id=account.id,
                         )
        cls.update_model_from_input(db_team, team)
        db.session.add(db_team)
        db.session.flush()  # Flush pending changes to generate the team's ID
        db.session.commit()
        
        return db_team
       
    @classmethod
    def update_team(cls, db, id, team, user, account):
        """
        Creates a new team with the provided configuration.

        Args:
            db: The database object.
            team_with_config: The object containing the team and configuration details.

        Returns:
            Team: The created team.

        """
        old_team = cls.get_team_by_id(db=db, team_id=id, account=account)
        if not old_team:
            raise TeamNotFoundException("Team not found")
        db_team = cls.update_model_from_input(team_model=old_team, team_input=team)
        db_team.modified_by = user.id
        
        db.session.add(db_team)
        db.session.commit()

        return db_team
     
    @classmethod
    def update_model_from_input(cls, team_model: TeamModel, team_input: TeamInput):
        for field in TeamInput.__annotations__.keys():
            setattr(team_model, field, getattr(team_input, field))
        return team_model  

    @classmethod
    def get_teams(cls, db, account):
        teams = (
            db.session.query(TeamModel)
            .filter(TeamModel.account_id == account.id, or_(or_(TeamModel.is_deleted == False, TeamModel.is_deleted is None), TeamModel.is_deleted is None))
            .all()
        )
        return teams
    

    @classmethod
    def get_team_by_id(cls, db, team_id, account):
        """
            Get Team from team_id

            Args:
                session: The database session.
                team_id(int) : Unique identifier of an Team.

            Returns:
                Team: Team object is returned.
        """
        # return db.session.query(TeamModel).filter(TeamModel.account_id == account.id, or_(or_(TeamModel.is_deleted == False, TeamModel.is_deleted is None), TeamModel.is_deleted is None)).all()
        teams = (
            db.session.query(TeamModel)
            .filter(TeamModel.id == team_id, or_(or_(TeamModel.is_deleted == False, TeamModel.is_deleted is None), TeamModel.is_deleted is None))
            .first()
        )
        return teams

    @classmethod
    def delete_by_id(cls, db, team_id, account):
        db_team = db.session.query(TeamModel).filter(TeamModel.id == team_id, TeamModel.account_id==account.id).first()

        if not db_team or db_team.is_deleted:
            raise TeamNotFoundException("Team not found")

        db_team.is_deleted = True
        db.session.commit()

    