  
import React, { Component } from 'react'

export default class Login extends Component {
    render() {
        return (
            <div>
                <div className="container-login100">
                    <div className="wrap-login100 p-l-110 p-r-110 p-t-62 p-b-33">
                        <form className="login100-form">
                            <span className="login100-form-title p-b-53">Sign In With</span>
                            <span>
                            <a href="#" className="btn-google">
                                <img src="images/icon-google.png" alt="GOOGLE" />
                                Google
                            </a>
                            </span>
                        </form>
                    </div>
                </div>
            </div>
        )
    }
}