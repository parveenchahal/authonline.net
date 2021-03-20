import './App.css';
import Login from './components/login'
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";

function App() {
  let args = {q: location.search}
  return (
    <Router>
      <Switch>
        <Route exact path="/login">
          <Login {...args}></Login>
        </Route>
      </Switch>
    </Router>
  );
}

export default App;
