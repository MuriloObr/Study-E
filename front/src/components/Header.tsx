/* eslint-disable camelcase */
import { Button } from '@/components/ui/button'
import { HoverCard, HoverCardContent, HoverCardTrigger } from './ui/hover-card'
export function Header({ user_id }: { user_id: int | undefined }) {
  return (
    <header className="relative h-20 w-full px-4 py-2 flex z-10 items-center justify-end">
      <h1 className="text-5xl w-fit inset-x-0 mx-auto absolute font-bold">Study-E</h1>
      {user_id ? (
        <HoverCard>
          <HoverCardTrigger>Usuario {user_id}</HoverCardTrigger>
          <HoverCardContent>Sobre usuário {user_id}</HoverCardContent>
        </HoverCard>
      ) : (
        <Button>Sign Up</Button>
      )}
    </header>
  )
}
