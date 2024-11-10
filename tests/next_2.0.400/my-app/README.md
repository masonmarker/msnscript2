## MSN2 NextJS Generator
As of the final release of 2.0.400, the NextJS generator will be available for use.
The NextJS generator offers a new way to program in the web. This implementation
translates MSN2 code into React code, and then into NextJS code. This allows for
the combination of server-side and client-side code in a single file. This also brings room
for the elimination of consideration for hooks and complex state management, as the
MSN2 NextJS generator handles all of this for you. This generator is still in development,
and is not yet ready for production. However, it is ready for testing, and is available
for use.

# Starting the Development Server for MSN2
To start the development server, run the following command from the my-app/ directory:
```bash
npm run dev
```
To update the NextJS application with the current MSN2 code while the dev server is running, run the following command from the root directory: msnscript2/   in a new terminal window: 
```bash
{python-alias} msn2cli.py -f tests/next_2.0.400/my-app/msn2/update
```

This is a [Next.js](https://nextjs.org/) project bootstrapped with [`create-next-app`](https://github.com/vercel/next.js/tree/canary/packages/create-next-app).

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `pages/index.jsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/basic-features/font-optimization) to automatically optimize and load Inter, a custom Google Font.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js/) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/deployment) for more details.