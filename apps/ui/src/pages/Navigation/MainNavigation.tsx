import { useEffect, useState } from 'react'
import styled from 'styled-components'

import HomeIconSvg from 'assets/svgComponents/HomeIconSvg'
import Games from '@l3-lib/ui-core/dist/icons/Games'
import Players from '@l3-lib/ui-core/dist/icons/Players'
import Collection from '@l3-lib/ui-core/dist/icons/Collection'

import { useLocation, useNavigate } from 'react-router-dom'
import { includes } from 'lodash'

const MainNavigation = () => {
  const navigate = useNavigate()

  const { pathname } = useLocation()

  const [active, setActive] = useState<string[]>([])

  const onHandleClick = (navigation_name: string) => {
    // setActive(navigation_name)
    navigate(navigation_name)
  }

  useEffect(() => {
    const pathArr = pathname ? pathname.split('/') : []

    setActive(pathArr)
  }, [pathname])

  return (
    <StyledUl>
      <StyledLi isActive={active[1] === ''} onClick={() => onHandleClick('')}>
        <HomeIconSvg />
        <span>Home</span>
      </StyledLi>
      <StyledLi isActive={includes(active, 'agents')} onClick={() => onHandleClick('agents')}>
        <Players />
        <span>Agents</span>
      </StyledLi>
      <StyledLi
        isActive={includes(active, 'datasources')}
        onClick={() => onHandleClick('datasources')}
      >
        <Collection />
        <span>Datasources</span>
      </StyledLi>
      <StyledLi isActive={includes(active, 'tools')} onClick={() => onHandleClick('tools')}>
        <Games />
        <span>Tools</span>
      </StyledLi>
    </StyledUl>
  )
}

export default MainNavigation

const StyledUl = styled.ul`
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  gap: 16px;
`
const StyledLi = styled.li<{ isActive?: boolean }>`
  width: 90px;
  height: 64px;
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  gap: 5px;
  cursor: pointer;
  span {
    font-size: 14px;
    font-weight: 500;
    line-height: 16px;
    color: var(--content-content-tertiary, rgba(255, 255, 255, 0.6));
  }
  opacity: 0.8;
  ${({ isActive }) =>
    isActive &&
    `
    opacity: 1;
    border-radius: 6px;
    background: var(--basic-foreground-black-1, rgba(0, 0, 0, 0.10));
    span{
      color: var(--content-content-primary, #FFF);
    }
    svg{
      path{
        fill-opacity: 1
      }
    }
`}
`
