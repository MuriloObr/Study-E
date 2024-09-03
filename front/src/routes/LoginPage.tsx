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
import { Link } from 'react-router-dom'

const formSchema = z.object({
  username: z.string(),
  password: z.string(),
})

export function LoginPage() {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
  })

  function onSubmit(values: z.infer<typeof formSchema>) {
    console.log(values)
  }

  return (
    <main className="w-full h-screen flex items-center justify-center">
      <Form {...form}>
        <form
          onSubmit={form.handleSubmit(onSubmit)}
          className="w-1/4 p-16 flex flex-col items-center gap-5 border rounded-xl"
        >
          <h1 className="text-4xl font-bold mb-8">Login</h1>
          <FormField
            control={form.control}
            name="username"
            render={({ field }) => (
              <FormItem className="w-4/5">
                <FormLabel className="text-xl">Email or Username</FormLabel>
                <FormControl>
                  <Input {...field} type="email" className="text-xl" />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="password"
            render={({ field }) => (
              <FormItem className="w-4/5">
                <FormLabel className="text-xl">Password</FormLabel>
                <FormControl>
                  <Input type="password" {...field} className="text-xl" />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <div className="grid grid-cols-3 gap-2 w-4/5">
            <Button type="submit" className="p-5 col-span-2">
              Login
            </Button>
            <Button className="p-5" variant={'secondary'} asChild>
              <Link to={'/register'}>Register</Link>
            </Button>
          </div>
        </form>
      </Form>
    </main>
  )
}
