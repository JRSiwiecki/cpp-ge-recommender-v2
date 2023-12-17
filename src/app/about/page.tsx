const linkStylingClasses = `text-center text-l 
        text-yellow-400 flex items-center m-2 underline transition duration-300 hover:text-green-800`;

export default function Page() {
  return (
    <main className="flex min-h-screen flex-col items-center bg-neutral-900 p-3">
      <h1 className="text-center text-4xl text-white">About</h1>

      <section>
        <h2 className="m-1 text-center text-2xl text-white">Creator</h2>
        <p className="m-1 text-center text-white">
          Made by <strong>Joseph Siwiecki</strong>
        </p>

        <div className="flex">
          <a
            className={linkStylingClasses}
            href="https://www.linkedin.com/in/josephsiwiecki/"
            target="_blank"
            rel="noopener noreferrer"
          >
            LinkedIn
          </a>

          <a
            className={linkStylingClasses}
            href="https://github.com/JRSiwiecki/cpp-ge-recommender-v2"
            target="_blank"
            rel="noopener noreferrer"
          >
            Github Repository
          </a>
        </div>
      </section>

      <section>
        <h2 className="m-1 text-center text-2xl text-white">
          Frameworks & Libraries
        </h2>

        <div className="flex">
          <a
            className={linkStylingClasses}
            href="https://create.t3.gg/"
            target="_blank"
            rel="noopener noreferrer"
          >
            T3 Stack
          </a>

          <a
            className={linkStylingClasses}
            href="https://nextjs.org/"
            target="_blank"
            rel="noopener noreferrer"
          >
            Next.js
          </a>

          <a
            className={linkStylingClasses}
            href="https://trpc.io/"
            target="_blank"
            rel="noopener noreferrer"
          >
            tRPC
          </a>

          <a
            className={linkStylingClasses}
            href="https://tailwindcss.com/"
            target="_blank"
            rel="noopener noreferrer"
          >
            Tailwind
          </a>

          <a
            className={linkStylingClasses}
            href="https://vercel.com/blog/what-is-vercel"
            target="_blank"
            rel="noopener noreferrer"
          >
            Vercel
          </a>

          <a
            className={linkStylingClasses}
            href="https://www.crummy.com/software/BeautifulSoup/"
            target="_blank"
            rel="noopener noreferrer"
          >
            BeautifulSoup
          </a>
        </div>
      </section>
    </main>
  );
}
