import { Header } from '@/components/Header'
import { useEffect } from 'react'
import { Outlet, useLoaderData, useNavigate } from 'react-router-dom'

export function Root() {
  const loaderData = useLoaderData() as { user_id: int | undefined }
  const navigate = useNavigate()
  useEffect(() => {
    navigate('/dashboard')
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  return (
    <div className="h-dvh flex flex-col">
      <Header user_id={loaderData.user_id} />
      <Outlet />
    </div>
  )
}
