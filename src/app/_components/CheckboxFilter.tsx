interface CheckboxFilterProps {
  name: string;
  label: string;
  checked: boolean;
  onChange: (newValue: boolean) => void;
}

const CheckboxFilter: React.FC<CheckboxFilterProps> = ({
  name,
  label,
  checked,
  onChange,
}) => {
  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    onChange(event.target.checked);
  };
  return (
    <div>
      <input
        type="checkbox"
        name={name}
        id={name.toLowerCase()}
        checked={checked}
        onChange={handleChange}
      />
      <label className="mx-2 text-white" htmlFor={name.toLowerCase()}>
        {label}
      </label>
    </div>
  );
};

export default CheckboxFilter;
