export default function NumberFilter() {
  return (
    <>
      <input
        type="number"
        name="Number of courses to display"
        id="number-of-courses"
        min={0}
        max={10}
        className="w-20 rounded-md border px-2 py-1"
      />
      <label className="mx-2 text-white" htmlFor="number-of-courses">
        Number of courses to display
      </label>
    </>
  );
}
