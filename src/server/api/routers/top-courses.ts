import latestCourseData from "src/data/course-data-2023.json";

import type {
  Course,
  Section,
  Area,
  CourseData,
} from "~/types/courseDataTypes";

import { z } from "zod";

import { createTRPCRouter, publicProcedure } from "~/server/api/trpc";

export const topCoursesRouter = createTRPCRouter({
  getTopCourses: publicProcedure
    .input(
      z.object({
        numberOfCourses: z.number(),
      }),
    )
    .query((options) => {
      const numberOfCourses = options.input.numberOfCourses;

      const topCourses: CourseData = latestCourseData;

      return { topCourses };
    }),
});
