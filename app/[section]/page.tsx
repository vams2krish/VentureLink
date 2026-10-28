import App from '../platform';
import {notFound} from 'next/navigation';
const pages=['dashboard','discovery','inbox','register','settings','admin','privacy'];
export default async function Page({params}:{params:Promise<{section:string}>}){const {section}=await params;if(!pages.includes(section))notFound();return <App initialPage={section}/>}
