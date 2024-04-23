import { type Metadata } from "next";

export const metadata: Metadata = {
  title: "CPP GE Recommender Top Courses",
  description: `Top Courses page for CPP GE Recommender, 
    containing the top GE courses by average GPA for each Area + Section at CPP.`,
};

export default function TopCoursesLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <section>{children}</section>;
}
