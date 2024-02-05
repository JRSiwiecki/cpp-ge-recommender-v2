import { api } from "~/trpc/server";

import type { TopCourses } from "~/types/courseDataTypes";

export const metadata = {
  title: "CPP GE Recommender Top Courses",
  description: `Top Courses page for CPP GE Recommender, 
    containing the top GE courses by average GPA for each Area + Section at CPP.`,
};

export default async function TopCourses() {
  const queryResult = await api.topCourses.getTopCourses.query();

  const topCourses: TopCourses = queryResult.topCourses;

  console.log(topCourses);

  return (
    <main className="flex min-h-screen flex-col items-center bg-neutral-900 p-3">
      <h1 className="text-center text-4xl text-white">Top Courses</h1>
      <div className="grid grid-cols-3 gap-1">
        {topCourses.areas.map((area) => (
          <div key={area.area} className="mx-2 my-3 rounded-md border p-2">
            <h2 className="text-xl font-semibold text-white">{area.area}</h2>
            <div className="grid grid-cols-3 gap-1">
              {area.sections.map((section) => (
                <div
                  key={section.section}
                  className="m-2 rounded-md border p-2"
                >
                  <h3 className="text-lg font-semibold text-white">
                    {section.section}
                  </h3>
                  <ul>
                    {section.courses.map((course) => (
                      <li
                        key={course.courseCode}
                        className="mx-2 my-3 text-white"
                      >
                        ⭐ {course.courseCode} - {course.averageGPA?.toFixed(2)}
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </main>
  );
}
