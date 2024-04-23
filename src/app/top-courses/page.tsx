"use client";

import { api } from "~/trpc/react";
import type { TopCourses } from "~/types/courseDataTypes";
import CheckboxFilter from "../_components/CheckboxFilter";
import NumberFilter from "../_components/NumberFilter";
import { useEffect, useState } from "react";

export default function TopCourses() {
  const [topCourses, setTopCourses] = useState<TopCourses | null>(null);
  const [displayedCourses, setDisplayedCourses] = useState<TopCourses | null>(
    null,
  );
  const [numCoursesToDisplay, setNumCoursesToDisplay] = useState(5);
  const [displayLanguage, setDisplayLanguage] = useState(false);
  const [displayHonors, setDisplayHonors] = useState(false);
  const [displayLabs, setDisplayLabs] = useState(false);
  const [displayActivities, setDisplayActivities] = useState(false);

  const queryResult = api.topCourses.getTopCourses.useQuery();

  useEffect(() => {
    setTopCourses(queryResult.data?.topCourses);
  }, [queryResult.data]);

  useEffect(() => {
    if (topCourses) {
      const filteredCourses: TopCourses = {
        areas: topCourses.areas.map((area) => ({
          area: area.area,
          sections: area.sections.map((section) => ({
            section: section.section,
            courses: section.courses.filter((course) => {
              const courseCode = course.courseCode.toLowerCase();
              const courseMarker = courseCode[courseCode.indexOf("-") - 2];

              return !(
                (!displayLanguage &&
                  ["chinese", "french", "spanish", "german"].some((language) =>
                    courseCode.includes(language),
                  )) ||
                (!displayHonors && courseMarker === "h") ||
                (!displayLabs && courseMarker === "l") ||
                (!displayActivities && courseMarker === "a")
              );
            }),
          })),
        })),
      };

      setDisplayedCourses(filteredCourses);
    }
  }, [
    topCourses,
    numCoursesToDisplay,
    displayLanguage,
    displayHonors,
    displayLabs,
    displayActivities,
  ]);

  return (
    <main className="flex min-h-screen flex-col items-center bg-neutral-900 p-3">
      <h1 className="text-center text-4xl text-white">Top Courses</h1>
      <section className="rounded-md border p-2">
        <h3 className="text-center text-xl font-semibold text-white">
          Filters
        </h3>
        <NumberFilter
          onChange={setNumCoursesToDisplay}
          value={numCoursesToDisplay}
        />
        <div className="flex flex-col">
          <CheckboxFilter
            name="DisplayLanguage"
            label="Display Language Classes"
            onChange={setDisplayLanguage}
            checked={displayLanguage}
          />
          <CheckboxFilter
            name="DisplayHonors"
            label="Display Honors Classes"
            onChange={setDisplayHonors}
            checked={displayHonors}
          />
          <CheckboxFilter
            name="Display Labs"
            label="Display Lab Classes"
            onChange={setDisplayLabs}
            checked={displayLabs}
          />
          <CheckboxFilter
            name="DisplayActivities"
            label="Display Activity Classes"
            onChange={setDisplayActivities}
            checked={displayActivities}
          />
        </div>
      </section>

      <div className="grid grid-cols-3 gap-1">
        {displayedCourses?.areas.map((area) => (
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
      <footer>
        <p className="text-center text-white">
          Note that section B3 contains no GEs.
        </p>
        <p className="text-center text-white">
          The courses shown are based on the 2023 CPP GE catalog.
        </p>
      </footer>
    </main>
  );
}
