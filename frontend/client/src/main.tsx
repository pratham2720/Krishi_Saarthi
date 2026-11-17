import { createRoot } from "react-dom/client";
import App from "./App";
import '@fontsource-variable/inter';
import '@fontsource-variable/material-symbols-outlined';
import 'leaflet/dist/leaflet.css';
import 'leaflet-draw/dist/leaflet.draw.css';
import 'leaflet-control-geocoder/dist/Control.Geocoder.css';
import "./index.css";

createRoot(document.getElementById("root")!).render(<App />);
