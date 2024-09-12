import React from 'react'
import ReactDOM from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import '../app/globals.css'
import { Root } from './routes/Root.tsx'
import { ErrorPage } from './ErrorPage.tsx'
import { Dashboard } from './routes/Dashboard.tsx'
import { LoginPage } from './routes/LoginPage.tsx'
import { RegisterPage } from './routes/RegisterPage.tsx'
import { Questions } from './routes/Questions.tsx'

const router = createBrowserRouter([
  {
    path: '/',
    element: <Root />,
    loader: () => ({ user_id: undefined }),
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
      {
        path: 'questions',
        element: <Questions />
      }
    ],
  },
])

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
)
