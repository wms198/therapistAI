import React from "react";
import AppointmentList from "./AppointmentList";
import { Appointments } from "./types";
import useFetch from "./UseFetch";
import AppointmentForm from "./AppointmentForm";
import { useState, useEffect } from 'react';

const Sidebar: React.FC = () => {
  // const [as, setA] = useState([]);
  // const addA = (a: never) => {
	// 	setA([...as:, a]);
	// };
  const {
    error,
    isPending,
    data: appointments,
  } = useFetch<Appointments[]>("http://localhost:8000/appointment/all");





  return (
    <div className="col-auto col-md-3 col-xl-2 px-sm-2 px-0 bg-dark">
      <div className="d-flex flex-column align-items-center align-items-sm-start px-3 pt-2 text-white min-vh-100">
        <a
          href="/"
          className="d-flex align-items-center pb-3 mb-md-0 me-md-auto text-white text-decoration-none"
        >
          <span className="fs-5 d-none d-sm-inline">See YOU</span>
        </a>

        <button className="btn btn-primary my-2">Make an appointment</button>
        {error && <div>{error}</div>}
        {isPending && <div>Loading...</div>}
        {appointments && <AppointmentList appointments={appointments} />}
      </div>
      <AppointmentForm />
    </div>
  );
};

export default Sidebar;
