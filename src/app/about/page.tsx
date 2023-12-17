export default function Page() {
  return (
    <main className="flex min-h-screen flex-col items-center bg-neutral-900 p-3">
      <h1 className="text-center text-4xl text-white">About</h1>

      <section>
        <h1>Creator</h1>
        <p>Made by Joseph Siwiecki</p>

        <a
          href="https://www.linkedin.com/in/josephsiwiecki/"
          target="_blank"
          rel="noopener noreferrer"
        >
          LinkedIn
        </a>

        <a
          href="https://github.com/JRSiwiecki/cpp-ge-recommender-v2"
          target="_blank"
          rel="noopener noreferrer"
        >
          Github Repository
        </a>
      </section>

      <section>
        <h2>Frameworks & Libraries</h2>

        <a
          href="https://create.t3.gg/"
          target="_blank"
          rel="noopener noreferrer"
        >
          T3 Stack
        </a>

        <a href="https://nextjs.org/" target="_blank" rel="noopener noreferrer">
          Next.js
        </a>

        <a href="https://trpc.io/" target="_blank" rel="noopener noreferrer">
          tRPC
        </a>

        <a
          href="https://tailwindcss.com/"
          target="_blank"
          rel="noopener noreferrer"
        >
          Tailwind
        </a>

        <a
          href="https://vercel.com/blog/what-is-vercel"
          target="_blank"
          rel="noopener noreferrer"
        >
          Vercel
        </a>

        <a
          href="https://www.crummy.com/software/BeautifulSoup/"
          target="_blank"
          rel="noopener noreferrer"
        >
          BeautifulSoup (Scraper)
        </a>
      </section>
    </main>
  );
}
