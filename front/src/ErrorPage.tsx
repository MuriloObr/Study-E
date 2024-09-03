import { Link, isRouteErrorResponse, useRouteError } from 'react-router-dom'
import { Button } from './components/ui/button'

export function ErrorPage() {
  const error = useRouteError()

  if (isRouteErrorResponse(error)) {
    return (
      <div className="w-full h-screen flex flex-col items-center justify-center gap-4">
        <h1 className="text-4xl font-bold">
          Oops! <span>{error.status}</span>
        </h1>
        <p className="text-xl italic">{error.statusText}</p>
        {error.data?.message && <span>{error.data.message}</span>}

        <Button asChild size={'default'}>
          <Link to={'/'}>Go Back to Home Page</Link>
        </Button>
      </div>
    )
  } else if (error instanceof Error) {
    return (
      <div>
        <h1>Oops! Unexpected Error</h1>
        <p>Something went wrong.</p>
        <p>
          <i>{error.message}</i>
        </p>
      </div>
    )
  } else {
    return <></>
  }
}
