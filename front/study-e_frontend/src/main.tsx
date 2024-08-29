import React from 'react'
import ReactDOM from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import { Dashboard } from './routes/Dashboard.tsx'
import { ErrorPage } from './ErrorPage.tsx'
import { LoginPage } from './routes/LoginPage.tsx'
import '../app/globals.css'
import { RegisterPage } from './routes/RegisterPage.tsx'
import { Root } from './routes/Root.tsx'

const router = createBrowserRouter([
  {
    path: '/',
    element: <Root />,
    loader: () => ({ user_id: 1 }),
    errorElement: <ErrorPage />,
    children: [
      {
        path: 'dashboard',
        element: <Dashboard />,
      },
      {
        path: 'login',
        element: <LoginPage />,
      },
      {
        path: 'register',
        element: <RegisterPage />,
      },
    ],
  },
])

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
)
