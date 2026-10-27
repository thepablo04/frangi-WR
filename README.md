# Frangi · calendario TP/SL

Registra varios trades por día, calcula el win rate por **trade** y sincroniza los registros entre el archivo local y la [página web actual](https://marketintel-nu.vercel.app/frangi/index.html) con una clave privada.

[Descargar el ZIP](https://github.com/thepablo04/frangi-WR/releases/download/v1.0.0/Frangi-sincronizado.zip) · [Código del calendario](https://github.com/thepablo04/frangi-WR/blob/main/frangi.html)

Para conservar marcas antiguas, extrae `frangi.html` y reemplaza tu archivo anterior **en la misma carpeta**; ábrelo con el mismo navegador. Pulsa **Sincronizar**. Puedes crear una clave `FR1-…` o introducir tu clave `MI1-…` de MarketIntel en **Iniciar calendario con esta clave**. En la otra PC o en la web, usa **Vincular este dispositivo** con la misma clave.

Los trades se guardan primero en el navegador, también sin conexión. Cuando hay internet, se envían cifrados. Los cambios hechos en equipos distintos se reúnen por identificador; si ambos editan el mismo trade, la página te pide elegir. El ZIP no incluye registros ni claves. **Descargar copia JSON** permite guardar un respaldo adicional.

La web y el archivo local usan el servicio de sincronización de [MarketIntel](https://marketintel-nu.vercel.app/) en Vercel. Este repositorio contiene la interfaz y el código del calendario; el servicio está alojado en el repositorio de MarketIntel. La misma clave `MI1` crea un espacio cifrado separado para Frangi, sin mezclar trades con el portafolio. Si el servicio no está disponible, los cambios locales permanecen guardados y se sincronizan al volver.

El HTML publicado se genera desde `source/` con `python scripts/build.py`. Para verificarlo ejecuta `python scripts/build.py --check` y `node --test tests/sync-core.test.cjs`.

El repositorio también está listo para GitHub Pages: en **Settings → Pages** elige **Deploy from a branch**, rama `main`, carpeta `/ (root)`. La página `descargar.html` y el calendario funcionarán desde ese dominio gracias al puente de sincronización ya publicado en Vercel.
