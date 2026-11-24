import { useState, useEffect } from "react";
import { socket } from '../socket';
import useFetch from "../UseFetch";
import Cookies from 'js-cookie';
import { ConnectionState } from '../components/ConnectionState';
import { ConnectionManager } from '../components/ConnectionManager';
import Button from "../components/Button/Button";

const Dashboard: React.FC = () => {
  const [response, setResponse] = useState<string>("");
  const [render, setRender] = useState<boolean>(false);
  const [isConnected, setIsConnected] = useState<boolean>(socket.connected);
  const [lastPong, setLastPong] = useState<string | null>(null);

  const keyDown = (e:  React.SyntheticEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {

        //Stops enter from creating a new line
        e.preventDefault();
        e.target = e.target.parentElement;
        handleSubmit(e);
        return true;
    }
  }

  const handleSubmit = (e: React.SyntheticEvent) => {
    e.preventDefault();
    const target = e.target as typeof e.target & {
      userMessage: { value: string };
    };
    const userContent = target.userMessage.value;
    target.userMessage.value = "";

    sendToLLM(userContent);
  };

  const sendToLLM = (userContent: string) => {
    socket.emit('userContent', {
      userContent: userContent,
      access_token: Cookies.get('access_token')
    });
    console.log("User content: ", userContent)

    // let location: string;
    // let method: string;
    // let body: string;
    // location = "http://localhost:8000/message/";
    // method = "POST";
    // body = JSON.stringify({ content: userContent });
    // fetch(location, {
    //   credentials: "include",
    //   method: method,
    //   headers: {
    //     "Content-Type": "application/json",
    //   },
    //   body: body,
    // })
    //   .then((response) => {
    //     interface FetchData {
    //       status: number;
    //       ok: boolean;
    //       json: { content: string }[];
    //     }

    //     return new Promise<FetchData>((resolve) =>
    //       response.json().then((json) =>
    //         resolve({
    //           status: response.status,
    //           ok: response.ok,
    //           json: json,
    //         })
    //       )
    //     );
    //   })
    //   .then(({ status, json, ok }) => {
    //     console.log("data/json:", json);
    //     console.log("status", status);
    //     console.log("ok:", ok);
    //     if (status == 200 && json.length > 1) {
    //       if (json !== undefined) {
    //         setResponse(json[1].content);
    //         setRender(true);
    //         setTimeout(() => {
    //           setRender(false);
    //         }, 2500);
    //       }
    //     }
    //   })
    //   .catch((error) => console.log("error:", error));
  };

  useEffect(() => {
    socket.on('connect', () => {
      console.log('connected')
      setIsConnected(true);
    });

    socket.on('disconnect', () => {
      console.log('disconnected')
      setIsConnected(false);
    });

    socket.on('pong', () => {
      console.log('pong')
      setLastPong(new Date().toISOString());
    });

    // socket.on('message', () => {
    //   console.log('message')
    // });

    return () => {
      socket.off('connect');
      socket.off('disconnect');
      socket.off('pong');
    };
  }, []);

  const sendPing = () => {
    const message = {
      id: 10,
      user: 'alex',
      time: Date.now(),
      data: 'test',
    };

    console.log('ping', message);
    // console.log('ping done');
    socket.emit('ping', message);
    // socket.send('hello');
  }

  return (
    <div className="col-8 py-3 mx-auto row col-xl-9" style={{ width: "50%" }}>
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
          <form onSubmit={handleSubmit} onKeyDown={keyDown}>
            <textarea
              className="form-control custom-control"
              rows={4}
              cols={72}
              id="userMessage"
            ></textarea>
            {/* <button
              className="btn btn-warning"
              style={{ width: "100%", marginTop: "24px" }}
            >
              send
            </button> */}
            <Button variant="primary"> send</Button>
          </form>
          
        </div>
      </div>
      <ConnectionState isConnected={isConnected}/>
      <div className='context-context'>
        <p>Connected: { '' + isConnected }</p>
        <p>Last pong: { lastPong || '-' }</p>
        <button onClick={ sendPing }>Send ping</button>
      </div>
    </div>
  );
};

export default Dashboard;
