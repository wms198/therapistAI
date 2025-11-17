import { Appointments } from "./types";

interface Props {
  appointments: Appointments[];
}

const AppointmentList = ({ appointments }: Props) => {
  return (
    <ul className="appoinments nav flex-column">
      {appointments.map((appointment) => (
        <li key={appointment.id}>
            <div className="d-flex justify-content-between">
                <div>{new Date(appointment.start_at).toLocaleString()}</div>
                 <div className="material-symbols-outlined" style={{ fontSize: "20px" }}>delete</div>
            </div>
        </li>
      ))}
    </ul>
  );
};
export default AppointmentList;
