import React from "react";

import { Routes, Route } from "react-router";
import "bootstrap/dist/css/bootstrap.min.css";

import Sidebar from "./Sidebar";
import Dashboard from "./Dashboard";
import Home from "./Home";
import SignUp from "./SignUp";

const App: React.FC = () => {
  return (
      <div className="container-fluid">
        <div className="row flex-nowrap">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/signup" element={<SignUp />} />
          </Routes>
        </div>
      </div>
  );
};

export default App;