export interface ServientregaGuiaInput {
  numFactura: string;
  nombreContacto: string;
  direccion: string;
  ciudad: string;
  departamento: string;
  telefono: string;
  correo: string;
  pesoKg: number;
  altoCm: number;
  anchoCm: number;
  largoCm: number;
  valorDeclarado: number;
  recaudoCOD?: number;
}

export async function generarGuiaServientrega(params: ServientregaGuiaInput): Promise<string> {
  const xmlPayload = `
    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
      <soap:Header>
        <AuthHeader xmlns="http://tempuri.org/">
          <login>${process.env.SERVIENTREGA_USER || ""}</login>
          <pwd>${process.env.SERVIENTREGA_PASSWORD || ""}</pwd>
          <Id_CodFacturacion>${process.env.SERVIENTREGA_COD_FACTURACION || "FACT-001"}</Id_CodFacturacion>
          <Nombre_Cargue>DESPACHO_ECOMMERCE</Nombre_Cargue>
        </AuthHeader>
      </soap:Header>
      <soap:Body>
        <CargueMasivoExterno xmlns="http://tempuri.org/">
          <envios>
            <CargueMasivoExternoDTO>
              <objEnvios>
                <EnviosExterno>
                  <Num_Guia>0</Num_Guia>
                  <Num_Piezas>1</Num_Piezas>
                  <Des_TipoTrayecto>1</Des_TipoTrayecto>
                  <Ide_Producto>2</Ide_Producto>
                  <Des_FormaPago>2</Des_FormaPago>
                  <Des_MedioTransporte>1</Des_MedioTransporte>
                  <Num_PesoTotal>${params.pesoKg}</Num_PesoTotal>
                  <Num_ValorDeclaradoTotal>${params.valorDeclarado}</Num_ValorDeclaradoTotal>
                  <Des_Telefono>${params.telefono}</Des_Telefono>
                  <Des_Ciudad>${params.ciudad.toUpperCase()}</Des_Ciudad>
                  <Des_Direccion>${params.direccion.toUpperCase()}</Des_Direccion>
                  <Nom_Contacto>${params.nombreContacto.toUpperCase()}</Nom_Contacto>
                  <Des_DiceContener>PRODUCTOS VARIOS</Des_DiceContener>
                  <idePaisOrigen>1</idePaisOrigen>
                  <idePaisDestino>1</idePaisDestino>
                  <Num_Alto>${params.altoCm}</Num_Alto>
                  <Num_Ancho>${params.anchoCm}</Num_Ancho>
                  <Num_Largo>${params.largoCm}</Num_Largo>
                  <Des_DepartamentoDestino>${params.departamento.toUpperCase()}</Des_DepartamentoDestino>
                  <Num_Factura>${params.numFactura}</Num_Factura>
                  <Des_CorreoElectronico>${params.correo}</Des_CorreoElectronico>
                  <Num_Recaudo>${params.recaudoCOD || 0}</Num_Recaudo>
                  <Est_EnviarCorreo>true</Est_EnviarCorreo>
                </EnviosExterno>
              </objEnvios>
            </CargueMasivoExternoDTO>
          </envios>
        </CargueMasivoExterno>
      </soap:Body>
    </soap:Envelope>
  `;

  const res = await fetch(process.env.SERVIENTREGA_GUIAS_URL || "http://web.servientrega.com:8081/GeneracionGuias.asmx", {
    method: "POST",
    headers: { "Content-Type": "text/xml; charset=utf-8" },
    body: xmlPayload
  });
  return await res.text();
}
