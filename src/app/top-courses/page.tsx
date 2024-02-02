import { api } from "~/trpc/server";

export default async function TopCourses() {
  const topCourses = await api.topCourses.getTopCourses.query({
    numberOfCourses: 5,
  });

  console.log(topCourses);

  return (
    <main className="flex min-h-screen flex-col items-center bg-neutral-900 p-3">
      <h1 className="text-center text-4xl text-white">Top Courses</h1>

      <div className="grid grid-cols-3 gap-1"></div>
    </main>
  );
}
