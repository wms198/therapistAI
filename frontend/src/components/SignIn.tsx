const SignIn: React.FC = () => {
    return (
        <>
            <div>
                <p className="text-primary">Sign in to See U</p>
                <p > Enter your details below</p>
            </div>
            <form>
                <p>Email</p>
                <input type="text" placeholder="Enter your e-mail" />
                <p>Password</p>
                <input type="text" />
                <button></button>
            </form>
        </>
    )
}

export default SignIn;