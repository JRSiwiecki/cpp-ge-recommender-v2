interface CheckboxFilterProps {
  name: string;
  label: string;
}

const CheckboxFilter: React.FC<CheckboxFilterProps> = ({ name, label }) => {
  return (
    <div>
      <input type="checkbox" name={name} id={name.toLowerCase()} />
      <label className="mx-2 text-white" htmlFor={name.toLowerCase()}>
        {label}
      </label>
    </div>
  );
};

export default CheckboxFilter;
