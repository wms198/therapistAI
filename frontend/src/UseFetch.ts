import { useState, useEffect } from 'react';
interface FetchResult<T>{
  data: T | null;
  isPending: Boolean;
  error: string | null
}


const useFetch = <T>(url: string, run:boolean=true, cacheBuster:number=0): FetchResult<T> => {
  const [data, setData] = useState(null);
  const [isPending, setIsPending] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {

    if(!run) return;
    const abortCont = new AbortController();

    setTimeout(() => {
      fetch(url, { signal: abortCont.signal })
      .then(res => {
        if (!res.ok) { // error coming back from server
          throw Error('could not fetch the data for that resource');
        } 
        return res.json();
      })
      .then(data => {
        setIsPending(false);
        setData(data);
        setError(null);
      })
      .catch(err => {
        if (err.name === 'AbortError') {
          console.log('fetch aborted')
        } else {
          // auto catches network / connection error
          setIsPending(false);
          setError(err.message);
        }
      })
    }, 1000);

    // abort the fetch
    return () => abortCont.abort();
  }, [url, run, cacheBuster])

  return { data, isPending, error };
}
 
export default useFetch;