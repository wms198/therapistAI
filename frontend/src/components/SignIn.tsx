import { Link } from 'react-router';

const SignIn: React.FC = () => {
    return (
        <>
            <div>
                <p>Register | <Link to={'/dashboard'}>As a guest</Link></p>
            </div>
            <p className="text-primary">Sign in to See U</p>
            <form action="http://localhost:8000/login" method='post'>
                <p>Email</p>
                <input type="text" placeholder="Enter your e-mail" name="email"/>
                <p>Password</p>
                <input type="text" name="password"/>
                <button>Login</button>
            </form>
        </>
    )
}

export default SignIn;