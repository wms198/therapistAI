import {Appointments} from "./types"

interface Props {
    appointments: Appointments[];
}

const AppointmentList = ({appointments}: Props) => {
    return(
        <ul className="nav nav-pills flex-column mb-sm-auto mb-0 align-items-center align-items-sm-start">
            {appointments.map((appointment) => (
                <li>{appointment.start_at}</li>
            ))}
        </ul>
    //     <a
    //         href="#submenu1"
    //         data-bs-toggle="collapse"
    //         className="nav-link px-0 align-middle"
    //         >
    //         <i className="fs-4 bi-speedometer2"></i>{" "}
    //         <span className="ms-1 d-none d-sm-inline">Hahahaha</span>{" "}
    //         </a>
    //         <ul
    //         className="collapse show nav flex-column ms-1"
    //         id="submenu1"
    //         data-bs-parent="#menu"
    //         ></ul>
    );
};
export default AppointmentList;