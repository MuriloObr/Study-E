import { Button } from '@/components/ui/button'
import {
  ListChecks,
  ChartNoAxesColumn,
  PencilLine,
  MessageSquareMore,
} from 'lucide-react'

export function Dashboard() {
  return (
    <main className="w-full flex-1 flex items-center justify-center">
      <ul className="grid grid-cols-2 grid-rows-3 gap-3 h-2/3 w-1/2">
        <Button className="w-full h-full row-span-2 text-6xl">
          Solve <PencilLine className="m-2" size={72} />
        </Button>
        <Button className="w-full h-full row-span-2 text-6xl">
          Review <ListChecks className="m-2" size={72} />
        </Button>
        <Button className="w-full h-50 text-4xl">
          Your Stats <ChartNoAxesColumn className="m-2" size={64} />
        </Button>
        <Button className="w-full h-50 text-4xl">
          Chat <MessageSquareMore className="m-2" size={64} />
        </Button>
      </ul>
    </main>
  )
}
