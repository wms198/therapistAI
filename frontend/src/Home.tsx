import { useState, useEffect } from "react";
import useFetch from "./UseFetch";

const Home: React.FC = () => {
  const [response, setResponse] = useState("");
  const [render, setRender] = useState(false);
  const handleSubmit = (e: React.SyntheticEvent) => {
    e.preventDefault();
    const target = e.target as typeof e.target & {
      userMessage: { value: string };
    };
    const userContent = target.userMessage.value;
    target.userMessage.value = "";
    console.log(userContent);
    sendToLLM(userContent);
  };

  const sendToLLM = (userContent: string) => {
    let location: string;
    let method: string;
    let body: string;
    location = "http://localhost:8000/message/";
    method = "POST";
    body = JSON.stringify({ content: userContent });
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
      .then(({ status, json, ok }) => {
        console.log("data/json:", json);
        console.log("status", status);
        console.log("ok:", ok);
        if (status == 200 && json.length > 1) {
          if (json !== undefined) {
            setResponse(json[1].content);

            setRender(true);
            setTimeout(() => {
              setRender(false);
            }, 2500);
          }
        }
      })
      .catch((error) => console.log("error:", error));
  };

  return (
    <div className="py-3 mx-auto row" style={{ width: "50%" }}>
      <div className="col align-self-center">
        <p
          className={
            (response ? "lead" : "lead text-center") +
            " " +
            (render ? "renderResponse" : "")
          }
          id="therapist"
        >
          {response ? response : "Hi. I'm here."}
        </p>
        {/* <div className="input-group position-relative"> */}
        <div className="d-flex flex-column ">
          <form onSubmit={handleSubmit}>
            <textarea
              className="form-control custom-control"
              rows={4}
              cols={72}
              id="userMessage"
            ></textarea>
            <button
              className="btn btn-warning"
              style={{ width: "100%", marginTop: "24px" }}
            >
              send
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};
export default Home;
