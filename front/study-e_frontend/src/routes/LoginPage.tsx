import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { Button } from '@/components/ui/button'

const formSchema = z.object({
  username: z.string(),
  password: z.string(),
})

export function LoginPage() {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
  })
  return (
    <main className="w-full h-screen flex items-center justify-center">
      <Form {...form}>
        <form className="w-1/4 p-16 flex flex-col items-center gap-5 border rounded-xl">
          <h1 className="text-4xl font-bold mb-8">Login</h1>
          <FormField
            control={form.control}
            name="username"
            render={({ field }) => (
              <FormItem className="w-2/3">
                <FormLabel className="text-xl">Username</FormLabel>
                <FormControl>
                  <Input {...field} className="text-xl" />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="password"
            render={({ field }) => (
              <FormItem className="w-2/3">
                <FormLabel className="text-xl">Password</FormLabel>
                <FormControl>
                  <Input type="password" {...field} className="text-xl" />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <div className="grid grid-cols-3 gap-2 w-2/3">
            <Button type="submit" className="p-5 col-span-2">
              Login
            </Button>
            <Button className="p-5" variant={'secondary'}>
              Register
            </Button>
          </div>
        </form>
      </Form>
    </main>
  )
}
