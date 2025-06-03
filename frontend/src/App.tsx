import React from "react";
import Sidebar from "./Sidebar";
import Home from "./Home";
import { BrowserRouter as Router, Route, Switch} from 'react-router-dom';
import "bootstrap/dist/css/bootstrap.min.css";

const App: React.FC = () => {
  return (
    <Router>
      <div className="container-fluid">
        <div className="row flex-nowrap">
          <Sidebar />
            <Switch>
              <Router>
                <Home />
              </Router>
            </Switch>
        </div>
      </div>
    </Router>
  )
}
  

export default App;


      {/* <div className="col-auto col-md-3 col-xl-2 px-sm-2 px-0 bg-dark">
          <div className="d-flex flex-column align-items-center align-items-sm-start px-3 pt-2 text-white min-vh-100">
            <a
              href="/"
              className="d-flex align-items-center pb-3 mb-md-0 me-md-auto text-white text-decoration-none"
            >
              <span className="fs-5 d-none d-sm-inline">See YOU</span>
            </a>
            <ul
              className="nav nav-pills flex-column mb-sm-auto mb-0 align-items-center align-items-sm-start"
              id="menu"
            >
              <li className="nav-item">
                <a href="#" className="nav-link align-middle px-0">
                  <i className="fs-4 bi-house"></i>{" "}
                  <span className="ms-1 d-none d-sm-inline">
                    Make an appointment
                  </span>
                </a>
              </li>
              <li>
                <a
                  href="#submenu1"
                  data-bs-toggle="collapse"
                  className="nav-link px-0 align-middle"
                >
                  <i className="fs-4 bi-speedometer2"></i>{" "}
                  <span className="ms-1 d-none d-sm-inline">Dashboard</span>{" "}
                </a>
                <ul
                  className="collapse show nav flex-column ms-1"
                  id="submenu1"
                  data-bs-parent="#menu"
                ></ul>
              </li>
            </ul>
          </div>
        </div> */}



        {/* <div className="py-3 mx-auto row" style={{ width: "50%" }}>
          <div className="col align-self-center">
            <p className="lead text-center" id="therapist">Hi. I'm here.</p>
            {/* <div className="input-group position-relative"> */}
        //     <div className="d-flex flex-column">
        //       <form onSubmit={handleSubmit} >
        //         <textarea
        //           className="form-control custom-control"
        //           rows={4}
        //           cols={72}
        //           id='textArea'
        //         >
        //         </textarea>
        //         <button
        //           className="btn btn-primary"
        //           style={{ width: "100%", marginTop: "24px" }}
        //         >
        //           send
        //         </button>
        //       </form>

        //     </div>
        //   </div>
        // </div> */}

 