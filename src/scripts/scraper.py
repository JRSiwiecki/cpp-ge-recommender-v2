import requests
import json
from bs4 import BeautifulSoup

# Only valid catalog urls, catalogs before 2021 have some varying structure that
# I will not be dealing with!
CATALOG_URLS = {
    2021: "https://catalog.cpp.edu/preview_program.php?catoid=57&poid=14912",
    2022: "https://catalog.cpp.edu/preview_program.php?catoid=61&poid=15936",
    2023: "https://catalog.cpp.edu/preview_program.php?catoid=65&poid=17161",
}


def scrape_cpp_data(catalog_year: int):
    """
    Scrapes CPP Course Catalog based on given catalog year and returns
    the resulting class areas (such as class areas A1, B2, C3).

    Args:
        catalog_year (str): Year to scrape the correct data for that catalog year.

    Returns:
        ResultSet[Any]: ResultSet containing the scraped data separated by class area.
    """

    if type(catalog_year) is not int:
        raise TypeError("Invalid input, catalog_year must be an int.")

    accepted_years = [2021, 2022, 2023]

    if catalog_year not in accepted_years:
        raise ValueError("Invalid catalog year.")

    url = CATALOG_URLS.get(catalog_year)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    class_areas = soup.find_all("div", class_="acalog-core")
    return class_areas


def categorize_courses(class_areas):
    # top element is current area
    area_stack = []

    # top element is current section
    section_stack = []

    # contains list of dicts containing sections in that area
    area_map = {}

    # contains list of classes in that section
    section_map = {}

    for class_area in class_areas:
        area = class_area.find("h2")
        section = class_area.find("h3")

        courses = class_area.find_all("li", class_="acalog-course")

        if area:
            # 5th index contains area letter
            area_stack.insert(0, area.text[5])
            current_area = area_stack[0]

            # edge case as these two don't have sections, just the area
            if current_area == "E":
                current_section = "0. Lifelong Learning and Self-Development"
                section_map[current_section] = []
            elif current_area == "F":
                current_section = "0. Ethnic Studies"
                section_map[current_section] = []

            area_map[current_area] = []

        if section:
            if "Note(s)" in section.text:
                break

            if "(" in section.text:
                end_marker = section.text.index("(") - 1
            else:
                end_marker = section.text.index(":")

            # 0th index contains section number
            section_stack.insert(0, section.text[0:end_marker])
            current_section = section_stack[0]

            section_map[current_section] = []
            area_map[current_area].append(section.text[0:end_marker])

        for course in courses:
            spans = course.find_all("span")

            for span in spans:
                if span:
                    end_marker = span.text.index("(")

                    section_map[current_section].append(span.text[0 : end_marker - 1])

    # hard code solution for E and F
    area_map["E"].append("0. Lifelong Learning and Self-Development")
    area_map["F"].append("0. Ethnic Studies")


def get_opencpp_api_data():
    response = requests.post("https://cpp-scheduler.herokuapp.com/data/courses/find")
    json_object = json.loads(response.text)
    return json_object


language_classes_filter = [
    "Chinese",
    "French",
    "Spanish",
    "German",
]


def recommend_course(area_section, area_map, section_map, json_object):
    requested_data = area_section

    if len(requested_data) < 2:
        response = {"Message": "Input too short."}
        return json.dumps(response)

    requested_area = requested_data[0].upper()
    requested_section = requested_data[1]

    accepted_area_sections = [
        "A1",
        "A2",
        "A3",
        "B1",
        "B2",
        "B4",
        "B5",
        "C1",
        "C2",
        "C3",
        "D1",
        "D2",
        "D4",
        "E",
        "F",
    ]

    if requested_area not in accepted_area_sections:
        response = {"Message": "Invalid area section."}

    if requested_area.isdigit():
        response = {"Message": "Area must be a letter."}
        return json.dumps(response)

    if requested_section.isalpha():
        response = {"Message": "Section must be a number."}
        return json.dumps(response)

    if requested_area not in area_map:
        response = {"Message": "Area does not exist."}
        return json.dumps(response)

    found_sections = area_map[requested_area]

    found_classes = []

    for section in found_sections:
        if requested_section in section:
            found_classes = section_map[section]
            break

    if not found_classes:
        response = {"Message": "No sections found."}
        return json.dumps(response)

    course_codes = []

    for found_class in found_classes:
        end_marker = found_class.index("-") - 1

        course_codes.append(found_class[0:end_marker])

    course_gpas = []

    for object in json_object:
        for course_code in course_codes:
            course_label = object["Label"]

            if course_code in course_label:
                course_title = object["CourseTitle"]

                if course_title is None:
                    course_title = get_course_title(found_class)

                # Remove Honors/Activity courses
                if course_title is not None and (
                    "Honors" in course_title or "Activity" in course_title
                ):
                    continue

                # Remove language courses but only when looking in C2 courses
                if area_section == "C2":
                    if course_title is not None and (
                        any(lang in course_title for lang in language_classes_filter)
                    ):
                        continue

                course_component = course_label[-1]

                if course_label is not None and (
                    "M" in course_component
                    or "H" in course_component
                    or "L" in course_component
                    or "A" in course_component
                ):
                    continue

                if object["AvgGPA"] is None:
                    course_gpas.append([course_code, course_title, 0])
                    continue

                course_avg_gpa = object["AvgGPA"]

                course_gpas.append(
                    [
                        course_code,
                        course_title,
                        round(float(course_avg_gpa), 2),
                    ]
                )

    course_gpas = sorted(course_gpas, key=lambda x: x[2], reverse=True)

    result_json = json.dumps(course_gpas)
    return result_json


def get_top_courses(area_map, section_map, json_object):
    top_courses = {}

    for area in area_map.keys():
        sections = area_map[area]

        for section in sections:
            found_classes = section_map[section]

            section_courses = []

            # Skip area section B3
            if area not in area_map or (
                area == "B" and section == "3. Laboratory Activity"
            ):
                continue

            for found_class in found_classes:
                end_marker = found_class.index("-") - 1
                course_code = found_class[0:end_marker]

                for object in json_object:
                    course_label = object["Label"]
                    course_title = object["CourseTitle"]

                    if course_title is None:
                        course_title = get_course_title(found_class)

                    # Remove Honors/Activity Courses
                    if course_code in course_label:
                        if course_title is not None and (
                            "Honors" in course_title or "Activity" in course_title
                        ):
                            continue

                        # Remove language courses but only when looking in C2 courses
                        if (
                            section
                            == "2. Literature, Modern Languages, Philosophy and Civilization"
                        ):
                            if course_title is not None and (
                                any(
                                    lang in course_title
                                    for lang in language_classes_filter
                                )
                            ):
                                continue

                        course_component = course_label[-1]

                        if course_label is not None and (
                            "M" in course_component
                            or "H" in course_component
                            or "L" in course_component
                            or "A" in course_component
                        ):
                            continue

                        course_average_gpa = object["AvgGPA"]

                        if course_average_gpa is None:
                            course_average_gpa = 0
                        else:
                            course_average_gpa = round(float(course_average_gpa), 2)

                        course_info = {
                            "CourseCode": course_code,
                            "CourseTitle": course_title,
                            "AvgGPA": course_average_gpa,
                        }

                        section_courses.append(course_info)

            section_courses = sorted(
                section_courses, key=lambda x: x["AvgGPA"], reverse=True
            )
            area_section_title = f"{area}{section}"
            top_courses[area_section_title] = section_courses[:5]

    result_json = json.dumps(top_courses)

    return result_json


# Used in case the data from OpenCPP API doesn't contain a course title
def get_course_title(full_course_name):
    # start 2 characters after the " - " separating class code from title
    start_marker = full_course_name.index("-") + 2

    return full_course_name[start_marker:]


def main():
    catalog_year = 2021
    class_areas = scrape_cpp_data(catalog_year)
    categorize_courses(class_areas)


if __name__ == "__main__":
    main()
