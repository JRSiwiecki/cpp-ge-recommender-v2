import Link from "next/link";

export default function navbar() {
  return (
    <div className="flex flex-grow flex-row justify-evenly bg-neutral-950 p-3">
      <Link
        href="/"
        className="rounded-md border p-2 text-center text-xl 
        text-yellow-400 transition duration-300 hover:bg-green-800"
      >
        Home
      </Link>

      <Link
        href="/"
        className="rounded-md border p-2 text-center text-xl 
        text-yellow-400 transition duration-300 hover:bg-green-800"
      >
        GE Recommender
      </Link>

      <Link
        href="/"
        className="rounded-md border p-2 text-center text-xl 
        text-yellow-400 transition duration-300 hover:bg-green-800"
      >
        Top Courses
      </Link>

      <Link
        href="/"
        className="rounded-md border p-2 text-center text-xl 
        text-yellow-400 transition duration-300 hover:bg-green-800"
      >
        About
      </Link>
    </div>
  );
}
