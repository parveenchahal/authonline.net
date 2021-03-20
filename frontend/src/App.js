import './App.css';
import Login from './components/login'
import {
  BrowserRouter as Router,
  Switch,
  Route,
} from "react-router-dom";

function App() {
  let qs = {qs: window.location.search}
  return (
    <Router>
      <Switch>
        <Route exact path="/login">
          <Login {...qs}></Login>
        </Route>
      </Switch>
    </Router>
  );
}

export default App;
