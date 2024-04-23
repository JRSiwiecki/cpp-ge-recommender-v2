interface NumberFilterProps {
  value: number;
  onChange: (newValue: number) => void;
}

const NumberFilter: React.FC<NumberFilterProps> = ({ value, onChange }) => {
  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = parseInt(event.target.value, 10);
    onChange(newValue);
  };

  return (
    <>
      <input
        type="number"
        value={value}
        onChange={handleChange}
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
};

export default NumberFilter;
