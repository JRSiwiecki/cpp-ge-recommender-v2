import Link from "next/link";

const linkStylingClasses = `rounded-md border p-2 text-center text-l 
        text-yellow-400 transition duration-300 hover:bg-green-800 flex items-center m-1`;

export default function navbar() {
  return (
    <div className="flex flex-grow flex-row justify-evenly bg-neutral-950 p-2">
      <Link href="/" className={linkStylingClasses}>
        Home
      </Link>

      <Link href="/" className={linkStylingClasses}>
        GE Recommender
      </Link>

      <Link href="/" className={linkStylingClasses}>
        Top Courses
      </Link>

      <Link href="/about" className={linkStylingClasses}>
        About
      </Link>
    </div>
  );
}
