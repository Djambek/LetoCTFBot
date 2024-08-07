import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import { AppRoot } from '@telegram-apps/telegram-ui';

ReactDOM.createRoot(document.getElementById('root')).render(
  <AppRoot>
    <App />
  </AppRoot>,
)
