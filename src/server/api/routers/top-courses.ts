import latestCourseData from "src/data/course-data-2023.json";

import type {
  Course,
  Section,
  Area,
  CourseData,
  TopCourses,
} from "~/types/courseDataTypes";

import { createTRPCRouter, publicProcedure } from "~/server/api/trpc";

export const topCoursesRouter = createTRPCRouter({
  getTopCourses: publicProcedure.query(() => {
    const topCourses: TopCourses = getTopCourses(latestCourseData);

    return { topCourses };
  }),
});

function getTopCourses(latestCourseData: CourseData): TopCourses {
  const topCourses: TopCourses = {
    areas: [],
  };

  const areas: Area[] = latestCourseData.areas;

  // Sort courses by averageGPA in descending order
  areas.forEach((currentArea: Area) => {
    const sections: Section[] = currentArea.sections;

    sections.forEach((currentSection: Section) => {
      currentSection.courses.sort((a: Course, b: Course) => {
        // If a class is null, treat its GPA as negative infinity to leave it at the bottom.
        const aGPA = a.averageGPA ?? Number.NEGATIVE_INFINITY;
        const bGPA = b.averageGPA ?? Number.NEGATIVE_INFINITY;

        return bGPA - aGPA;
      });
    });

    topCourses.areas.push(currentArea);
  });

  return topCourses;
}
