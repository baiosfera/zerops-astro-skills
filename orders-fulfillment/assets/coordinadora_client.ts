export interface CoordinadoraGuiaInput {
  idOrden: string;
  nombreDestinatario: string;
  direccionDestinatario: string;
  ciudadDane8: string;
  telefono: string;
  pesoKg: number;
  largoCm: number;
  anchoCm: number;
  altoCm: number;
  valorDeclarado: number;
  valorRecaudoCOD?: number;
}

export async function generarGuiaCoordinadora(params: CoordinadoraGuiaInput): Promise<string> {
  const xmlPayload = `
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ser="https://sandbox.coordinadora.com/agw/ws/guias/1.6/server.php">
      <soapenv:Header/>
      <soapenv:Body>
        <ser:Guias.generarGuia>
          <p>
            <codigo_remision></codigo_remision>
            <fecha>${new Date().toISOString().split("T")[0]}</fecha>
            <id_cliente>${process.env.COORDINADORA_ID_CLIENTE || "0"}</id_cliente>
            <nit_remitente>${process.env.COORDINADORA_NIT_REMITENTE || ""}</nit_remitente>
            <nombre_remitente>${process.env.COORDINADORA_NOMBRE_REMITENTE || ""}</nombre_remitente>
            <direccion_remitente>${process.env.COORDINADORA_DIR_REMITENTE || ""}</direccion_remitente>
            <telefono_remitente>${process.env.COORDINADORA_TEL_REMITENTE || ""}</telefono_remitente>
            <ciudad_remitente>${process.env.COORDINADORA_CIUDAD_DANE || "05001000"}</ciudad_remitente>
            <nombre_destinatario>${params.nombreDestinatario}</nombre_destinatario>
            <direccion_destinatario>${params.direccionDestinatario}</direccion_destinatario>
            <ciudad_destinatario>${params.ciudadDane8}</ciudad_destinatario>
            <telefono_destinatario>${params.telefono}</telefono_destinatario>
            <valor_declarado>${params.valorDeclarado}</valor_declarado>
            <codigo_cuenta>1</codigo_cuenta>
            <codigo_producto>0</codigo_producto>
            <nivel_servicio>1</nivel_servicio>
            <contenido>Artículos de Comercio Electrónico</contenido>
            <referencia>${params.idOrden}</referencia>
            <estado>IMPRESO</estado>
            <detalle>
              <item>
                <ubl>0</ubl>
                <alto>${params.altoCm}</alto>
                <ancho>${params.anchoCm}</ancho>
                <largo>${params.largoCm}</largo>
                <peso>${params.pesoKg}</peso>
                <unidades>1</unidades>
              </item>
            </detalle>
            ${
              params.valorRecaudoCOD
                ? `
            <recaudos>
              <item>
                <valor>${params.valorRecaudoCOD}</valor>
                <forma_pago>1</forma_pago>
              </item>
            </recaudos>`
                : ""
            }
            <formato_impresion>POS_PDF</formato_impresion>
            <usuario>${process.env.COORDINADORA_USER || ""}</usuario>
            <clave>${process.env.COORDINADORA_PASSWORD_SHA256 || ""}</clave>
          </p>
        </ser:Guias.generarGuia>
      </soapenv:Body>
    </soapenv:Envelope>
  `;

  const res = await fetch(process.env.COORDINADORA_GUIAS_URL || "https://sandbox.coordinadora.com/agw/ws/guias/1.6/server.php", {
    method: "POST",
    headers: { "Content-Type": "text/xml; charset=utf-8" },
    body: xmlPayload
  });
  return await res.text();
}
