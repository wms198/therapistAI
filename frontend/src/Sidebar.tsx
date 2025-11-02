import React, { use } from "react";
import AppointmentList from "./AppointmentList";
import { Appointments } from "./types";
import useFetch from "./UseFetch";
import AppointmentForm from "./AppointmentForm";
import { useState, useEffect } from "react";

const Sidebar: React.FC = () => {
  const [cacheBuster, setCacheBuster] = useState<number>(0);
  const {
    error,
    isPending,
    data: appointments,
  } = useFetch<Appointments[]>(
    "http://localhost:8000/appointment/",
    true,
    cacheBuster
  );
  return (
    <div className="col-2 px-sm-2 px-0 bg-dark min-vh-100 ">
      <div className="px-3 pt-2 text-white ">
        <span className="fs-3 navbar">See YOU</span>
        {/* <button className="btn btn-primary my-2">Make an appointment</button> */}
        {error && <div>{error}</div>}
        {isPending && <div>Loading...</div>}
        {appointments && <AppointmentList appointments={appointments} />}
      </div>
      {!isPending && (
        <AppointmentForm
          onSubmitSuccess={() => setCacheBuster(cacheBuster + 1)}
        />
      )}
    </div>
  );
};

export default Sidebar;
