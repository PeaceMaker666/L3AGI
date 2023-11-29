import { FormikProvider } from 'formik'
import DatasourceForm from './DatasourceForm'

import Button from '@l3-lib/ui-core/dist/Button'
import Loader from '@l3-lib/ui-core/dist/Loader'
import Typography from '@l3-lib/ui-core/dist/Typography'

import Play from '@l3-lib/ui-core/dist/icons/PlayOutline'

import {
  StyledHeaderGroup,
  StyledSectionDescription,
  StyledSectionTitle,
  StyledSectionWrapper,
} from 'pages/Home/homeStyle.css'

import ComponentsWrapper from 'components/ComponentsWrapper/ComponentsWrapper'
import { StyledButtonWrapper } from 'pages/Agents/AgentForm/CreateAgentForm'
import { useCreateDatasource } from '../useCreateDatasource'
import BackButton from 'components/BackButton'
import { ButtonPrimary, ButtonTertiary } from 'components/Button/Button'
import { t } from 'i18next'
import { StyledFormWrapper } from 'styles/formStyles.css'
import styled from 'styled-components'
import DemoButton from 'components/DemoButton'
import { useModal } from 'hooks'

const CreateDatasourceForm = () => {
  const { formik, isLoading } = useCreateDatasource()

  const { openModal } = useModal()

  return (
    <>
      <FormikProvider value={formik}>
        <StyledSectionWrapper>
          <StyledHeaderGroup className='header_group'>
            <div>
              <StyledSectionTitle>{`${t('add-datasource')}`}</StyledSectionTitle>
              <StyledSectionDescription>
                {`${t('datasource-description')}`}
              </StyledSectionDescription>
            </div>
            <StyledCustomButton>
              <DemoButton
                onClick={() =>
                  openModal({
                    name: 'video-modal',
                    data: { videoSrc: import.meta.env.REACT_APP_YOUTUBE_VIDEO_DATA_SOURCE_ID },
                  })
                }
              />
            </StyledCustomButton>

            <StyledButtonWrapper>
              <BackButton />
              <ButtonPrimary
                onClick={formik?.handleSubmit}
                size={Button.sizes.SMALL}
                disabled={isLoading}
              >
                {isLoading ? <Loader size={32} /> : 'Save'}
              </ButtonPrimary>
            </StyledButtonWrapper>
          </StyledHeaderGroup>

          <ComponentsWrapper noPadding>
            <StyledFormWrapper>
              <DatasourceForm formik={formik} isLoading={isLoading} />
            </StyledFormWrapper>
          </ComponentsWrapper>
        </StyledSectionWrapper>
      </FormikProvider>
    </>
  )
}

export default CreateDatasourceForm

const StyledCustomButton = styled.div`
  margin-right: auto;
`
