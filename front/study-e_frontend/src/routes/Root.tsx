import { Header } from '@/components/Header'
import { Outlet, useLoaderData } from 'react-router-dom'

export function Root() {
  const loaderData = useLoaderData() as { user_id: int | undefined }
  return (
    <>
      <Header user_id={loaderData.user_id} />
      <Outlet />
    </>
  )
}
