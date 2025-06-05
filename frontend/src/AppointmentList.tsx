import {Appointments} from "./types"

interface Props {
    appointments: Appointments[];
}

const AppointmentList = ({appointments}: Props) => {
    return(
        <ul className="nav nav-pills flex-column mb-sm-auto mb-0 align-items-center align-items-sm-start">
            {appointments.map((appointment) => (
                <li>{appointment.start_at.replace("T", " ").replace("Z", "")}</li>
            ))}
        </ul>
    );
};
export default AppointmentList;