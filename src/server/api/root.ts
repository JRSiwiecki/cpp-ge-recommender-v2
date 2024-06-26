import { createTRPCRouter } from "~/server/api/trpc";
import { topCoursesRouter } from "./routers/top-courses";

/**
 * This is the primary router for your server.
 *
 * All routers added in /api/routers should be manually added here.
 */
export const appRouter = createTRPCRouter({
  topCourses: topCoursesRouter,
});

// export type definition of API
export type AppRouter = typeof appRouter;
