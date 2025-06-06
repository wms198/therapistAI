import { useState } from "react";
import { AddAppointment } from "./types";
type onSuccessCallback = () => void;
interface Props {
  onSubmitSuccess: onSuccessCallback;
}

const AppointmentForm = ({onSubmitSuccess}:Props) => {
  const [date, setDate] = useState("");
  const handleSubmit = (e: React.SyntheticEvent) => {
    e.preventDefault();
    const target = e.target as typeof e.target & {
      newAppointmentDate: { value: string };
    };
    const newAppointmentDate = new Date(target.newAppointmentDate.value);
    console.log(newAppointmentDate);
    addAppointment(newAppointmentDate.toISOString());
	//target.newAppointmentDate.value = ""
    setDate("")
    onSubmitSuccess()
  };

  const handleInput = (e: React.SyntheticEvent) => {
	const target = e.target as typeof e.target & { value: string };
	setDate(target.value)
  }

  const addAppointment = (date: string) => {
    let location: string;
    let method: string;
    let body: string;
    location = "http://localhost:8000/appointment/";
    method = "POST";
    body = JSON.stringify({ start_at: date });
    fetch(location, {
      credentials: "include",
      method: method,
      headers: {
        "Content-Type": "application/json",
      },
      body: body,
    })
      .then((response) => {
        interface FetchData {
          status: number;
          ok: boolean;
          json: { content: string }[];
        }

        return new Promise<FetchData>((resolve) =>
          response.json().then((json) =>
            resolve({
              status: response.status,
              ok: response.ok,
              json: json,
            })
          )
        );
      })
      .catch((error) => console.log("error:", error));
  };

  return (
    <div className="container appointment-form">
      <form onSubmit={ handleSubmit }>
        <input
          className="btn btn-outline-warning w-100 mb-2 "
          type="submit"
          value="Add Appointment"
        />
        <input
          type="datetime-local"
          className="w-100"
          id="newAppointmentDate"
          onChange={ handleInput }
          value={date}  
        />
      </form>
    </div>
  );
};

export default AppointmentForm;
