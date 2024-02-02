const linkStylingClasses = `text-center text-l 
        text-yellow-400 flex items-center m-2 
        underline transition duration-300 
        hover:text-green-800`;

const headerStylingClasses = `m-3 text-center text-3xl text-white`;

const linkHolderStylingClasses = `flex justify-center`;

export const metadata = {
  title: "CPP GE Recommender About",
  description: `About page for CPP GE Recommender, 
    containing information on how this application was created and the credits due.`,
};

export default function Page() {
  return (
    <main className="flex min-h-screen flex-col items-center bg-neutral-900 p-3">
      <h1 className="mb-10 text-center text-4xl text-white">About</h1>

      <section>
        <h2 className="m-1 text-center text-3xl text-white">Creator</h2>
        <p className="m-1 text-center text-white">Made by Joseph Siwiecki</p>

        <div className="flex justify-center">
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
        <h2 className={headerStylingClasses}>Frameworks & Libraries</h2>

        <div className={linkHolderStylingClasses}>
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

        <section>
          <h2 className={headerStylingClasses}>Data</h2>

          <div className={linkHolderStylingClasses}>
            <a
              className={linkStylingClasses}
              href="https://catalog.cpp.edu/preview_program.php?catoid=53&poid=13914"
              target="_blank"
              rel="noopener noreferrer"
            >
              California State Polytechnic University, Pomona - General
              Education Course List
            </a>

            <a
              className={linkStylingClasses}
              href="https://github.com/ZombiMigz/opencpp-api"
              target="_blank"
              rel="noopener noreferrer"
            >
              ZombiMigz - OpenCPP API
            </a>
          </div>
        </section>

        <section>
          <h2 className={headerStylingClasses}>Other Helpful Applications</h2>

          <div className={linkHolderStylingClasses}>
            <a
              className={linkStylingClasses}
              href="https://www.cppscheduler.com/"
              target="_blank"
              rel="noopener noreferrer"
            >
              ZombiMigz - CPPScheduler.com
            </a>

            <a
              className={linkStylingClasses}
              href="https://broncodirect.me/"
              target="_blank"
              rel="noopener noreferrer"
            >
              CPP CS Discord - BroncoDirectMe Extension
            </a>
          </div>
        </section>
      </section>

      <footer>
        <section>
          <p className="text-white">Not affiliated with CPP.</p>
        </section>
      </footer>
    </main>
  );
}
