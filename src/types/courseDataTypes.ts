export type Course = {
  courseCode: string;
  averageGPA: number | null;
};

export type Section = {
  section: string;
  courses: Course[];
};

export type Area = {
  area: string;
  sections: Section[];
};

export type CourseData = {
  year: number;
  areas: Area[];
};
