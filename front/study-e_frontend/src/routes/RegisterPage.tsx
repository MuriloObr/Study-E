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

const formSchema = z
  .object({
    name: z.string(),
    username: z.string().trim(),
    email: z.string().email('This is not a valid email').trim(),
    confirmEmail: z.string().trim(),
    password: z
      .string()
      .min(8, 'Password need min 8 chars')
      .regex(/\d+/, 'Password must have a number')
      .regex(
        /[!@#$%^&*()_+\-={}[\]:;"'<>,.?/|`~]/,
        'Password must have a symbol',
      )
      .trim(),
    confirmPass: z.string().trim(),
  })
  .refine(({ password, confirmPass }) => password === confirmPass, {
    message: 'Passwords must match each other',
    path: ['confirmPass'],
  })
  .refine(({ email, confirmEmail }) => email === confirmEmail, {
    message: 'Emails must match each other',
    path: ['confirmEmail'],
  })

export function RegisterPage() {
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
          className="w-2/4 p-16 grid grid-cols-2 justify-items-center gap-5 border rounded-xl"
        >
          <h1 className="text-4xl font-bold mb-8 col-span-2">Register</h1>
          <FormField
            control={form.control}
            name="name"
            render={({ field }) => (
              <FormItem className="w-4/5">
                <FormLabel className="text-xl">Name</FormLabel>
                <FormControl>
                  <Input {...field} type="text" className="text-xl" />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="username"
            render={({ field }) => (
              <FormItem className="w-4/5">
                <FormLabel className="text-xl">Username</FormLabel>
                <FormControl>
                  <Input {...field} type="text" className="text-xl" />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="email"
            render={({ field }) => (
              <FormItem className="w-4/5">
                <FormLabel className="text-xl">Email</FormLabel>
                <FormControl>
                  <Input {...field} type="email" className="text-xl" />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="confirmEmail"
            render={({ field }) => (
              <FormItem className="w-4/5">
                <FormLabel className="text-xl">Confirm Email</FormLabel>
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
              <FormItem className="w-4/5">
                <FormLabel className="text-xl">Password</FormLabel>
                <FormControl>
                  <Input type="password" {...field} className="text-xl" />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="confirmPass"
            render={({ field }) => (
              <FormItem className="w-4/5">
                <FormLabel className="text-xl">Confirm Password</FormLabel>
                <FormControl>
                  <Input type="password" {...field} className="text-xl" />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <div className="col-span-2 grid grid-cols-3 gap-2 w-3/5">
            <Button type="submit" className="p-5 col-span-2">
              Register
            </Button>
            <Button className="p-5" variant={'secondary'}>
              <Link to={'/login'}>Login</Link>
            </Button>
          </div>
        </form>
      </Form>
    </main>
  )
}
