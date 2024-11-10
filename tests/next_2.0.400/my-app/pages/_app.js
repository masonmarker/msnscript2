// Generated at 1729103274.4568117
// appwide styles
import '../styles/app.css'

// imports ::
import { ChakraProvider } from '@chakra-ui/react';

// main app component
function MyApp({ Component, pageProps }) {
return (
// return ::
<ChakraProvider>

<Component {...pageProps} />
{/** endreturn */}
</ChakraProvider>

)}

export default MyApp
