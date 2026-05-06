import React from "react";

import { Routes, Route } from "react-router";

import Sidebar from "./components/Sidebar";
import Dashboard from "./components/Dashboard";
import Home from "./components/Home";
import SignUp from "./components/SignUp";

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